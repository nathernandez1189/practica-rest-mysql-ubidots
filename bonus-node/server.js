// Mismo contrato HTTP de Flask, implementado en JavaScript con MySQL.
const http = require('node:http');
const mysql = require('mysql2/promise');
const pool = mysql.createPool({host:process.env.MYSQL_HOST || '127.0.0.1',
  port:Number(process.env.MYSQL_PORT || 3306), user:process.env.MYSQL_USER || 'rest_equipo',
  password:process.env.MYSQL_PASSWORD, database:process.env.MYSQL_DB || 'rest_equipo',
  charset:'utf8mb4', connectionLimit:4});
const fields=['title','description','author'];
function valid(data, create){
  return data && !Array.isArray(data) && typeof data==='object' && Object.keys(data).length>0 &&
    (!create || Object.prototype.hasOwnProperty.call(data,'title')) && Object.keys(data).every(k=>fields.includes(k)) &&
    Object.values(data).every(v=>typeof v==='string' && [...v].length<=255) &&
    (!Object.prototype.hasOwnProperty.call(data,'title') || data.title.trim().length>0);
}
const server=http.createServer(async(req,res)=>{
  const send=(code,data,headers={})=>{res.writeHead(code,{'Content-Type':'application/json; charset=utf-8',...headers});res.end(JSON.stringify(data));};
  try {
    const path=new URL(req.url,'http://localhost').pathname;
    if(path==='/health' && req.method==='GET') {await pool.query('SELECT 1');return send(200,{status:'ok',storage:'MySQL-JavaScript'});}
    const match=path.match(/^\/books(?:\/(\d+))?$/);
    if(!match) return send(404,{error:'Ruta no encontrada'});
    const id=match[1] ? Number(match[1]) : null;
    if(req.method==='GET'){
      const [rows]=await pool.execute(id===null?'SELECT * FROM books ORDER BY id':'SELECT * FROM books WHERE id=?',id===null?[]:[id]);
      return id===null?send(200,{books:rows}):rows.length?send(200,{book:rows[0]}):send(404,{error:'Libro no encontrado'});
    }
    if(req.method==='POST' && id===null || req.method==='PUT' && id!==null){
      let raw='';for await(const chunk of req){raw+=chunk;if(Buffer.byteLength(raw)>16384)return send(413,{error:'Cuerpo demasiado grande'});}
      let body;try{body=JSON.parse(raw);}catch{return send(400,{error:'JSON inválido'});}
      if(!valid(body,req.method==='POST'))return send(400,{error:'Campos inválidos'});
      if(req.method==='POST'){
        const book={title:body.title,description:body.description||'',author:body.author||''};
        const [result]=await pool.execute('INSERT INTO books(title,description,author) VALUES(?,?,?)',fields.map(k=>book[k]));
        book.id=result.insertId;return send(201,{book},{Location:'/books/'+book.id});
      }
      const conn=await pool.getConnection();
      try{
        await conn.beginTransaction();
        const [rows]=await conn.execute('SELECT * FROM books WHERE id=? FOR UPDATE',[id]);
        if(!rows.length){await conn.rollback();return send(404,{error:'Libro no encontrado'});}
        const book={...rows[0],...body};
        await conn.execute('UPDATE books SET title=?,description=?,author=? WHERE id=?',[book.title,book.description,book.author,id]);
        await conn.commit();return send(200,{book});
      }catch(e){await conn.rollback();throw e;}finally{conn.release();}
    }
    if(req.method==='DELETE' && id!==null){const [result]=await pool.execute('DELETE FROM books WHERE id=?',[id]);return result.affectedRows?send(200,{result:true}):send(404,{error:'Libro no encontrado'});}
    return send(405,{error:'Método no permitido'});
  }catch(err){console.error('Error de base de datos:',err.code || err.name);send(503,{error:'Base de datos no disponible'});}
});
server.listen(Number(process.env.PORT || 5002),'0.0.0.0',()=>console.log('API JavaScript lista en puerto '+(process.env.PORT || 5002)));
