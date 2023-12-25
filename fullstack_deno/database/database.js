import { postgres } from "../deps.js";

let sql;
if (Deno.env.get("DATABASE_URL")) {
  sql = postgres(Deno.env.get("DATABASE_URL"));
} else {
  sql = postgres({
    host: Deno.env.get('CONTAINER_IP'), 
    port: Deno.env.get('PORT'), 
    database: Deno.env.get('DATABASE'), 
    user: Deno.env.get('USER'), 
    password: Deno.env.get('PASS_WORD') 
  });
}

export { sql };
