import { sql } from "../database/database.js";

const addTopic = async (userId, name) => {
    return await sql`INSERT INTO topics (user_id, name) VALUES (${userId}, ${name})`;
};

const getTopicsCount = async () => {
    const result = await sql`SELECT count(id) FROM topics`;
    return result[0].count;
    
};

const getTopicsAll = async () => {
    return await sql`SELECT * FROM topics ORDER BY name ASC`;
};

const getTopicsByUserId = async (userId) => {
    return await sql`SELECT * FROM topics WHERE user_id = ${userId}`;
};

const getTopicsByTopicId = async (id) => {
    return await sql`SELECT * FROM topics WHERE id=${id}`;
};

const deleteTopic = async (id) => {
    return await sql`DELETE FROM topics WHERE id=${id}`;
};


export { addTopic, getTopicsCount, getTopicsAll, getTopicsByUserId,getTopicsByTopicId,deleteTopic };