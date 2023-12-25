import { app } from "./app.js";

const DEFAULT_PORT = 7777;
const port = Deno.args.length > 0 ? Number(Deno.args[Deno.args.length - 1]) : DEFAULT_PORT;

app.listen({ port });
