import { sql } from "../database/database.js";

const getQuestionCount = async () => {
  const result = await sql`SELECT count(id) as count FROM questions`;
  return result[0].count;
};

const getQuestionsByTopicId = async (topicId) => {
  return await sql`SELECT * FROM questions WHERE topic_id=${topicId}`;
};

const getQuestionByQuestionID = async (id) => {
  return await sql`SELECT * FROM questions WHERE id = ${id}`;
  
};

const addQuestion = async (userId, topicId, questionText) => {
  return await sql`INSERT INTO questions (user_id, topic_id, question_text) VALUES (${userId},${topicId},${questionText})`;
};

const deleteQuestion = async (id) => {
  return await sql`DELETE FROM questions WHERE id=${id}`;
};

const getRandomQuestion = async (tid) => {
  const res = await sql`SELECT * FROM questions WHERE topic_id=${tid} ORDER BY RANDOM() LIMIT 1;`;

  if (res && res.length > 0) {
    return res[0];
  } else {
    return null;
  }
};


const getRandomQuestionAPI = async () => {
  const res = await sql`SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;`;

  if (res && res.length > 0) {
    return res[0];
  } else {
    return null;
  }
};


export { addQuestion, getQuestionCount, getQuestionsByTopicId, getQuestionByQuestionID, deleteQuestion, getRandomQuestion, getRandomQuestionAPI };