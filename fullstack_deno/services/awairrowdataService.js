import sql from "../database/database.js";

const findAll = async () => {
    const result = await sql`SELECT * FROM awair_data`;
    return result;
};
export { findAll };
