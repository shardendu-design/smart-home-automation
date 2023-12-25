import { sql } from "../database/database.js";

const getQuestionAnswersCount = async () => {
    const result = await sql`SELECT count(id) FROM question_answer_options`;
    return result[0].count;
    
};

const getAnswerByQuestionId = async (id) => {
    return await sql`SELECT * FROM question_answer_options WHERE question_id=${id}`;
};

const addAnswerOptions = async (id, optionText, isCorrect) => {
    return await sql`
        INSERT INTO question_answer_options (question_id, option_text, is_correct)
        VALUES (${id}, ${optionText}, ${isCorrect})
    `;
};

const deleteAnswerOption = async (questionId, Id) => {
    return await sql`DELETE FROM question_answer_options WHERE question_id=${questionId} AND id=${Id}`;
};

const deleteAnswerByOptionId = async (optionId) => {
    return await sql`DELETE FROM question_answers WHERE question_answer_option_id=${optionId}`;
}

const getCorrectOption = async (questionId) => {
  return await sql`SELECT * FROM question_answer_options WHERE question_id = ${questionId} AND is_correct = true`;
};
const storePostAnswer = async (userId, questionId, optionId) => {
    return await sql`INSERT INTO question_answers (user_id, question_id, question_answer_option_id) VALUES (${userId}, ${questionId}, ${optionId})`;
};

export {
    addAnswerOptions,
    getQuestionAnswersCount,
    getAnswerByQuestionId,
    deleteAnswerOption,
    getCorrectOption,
    storePostAnswer,
    deleteAnswerByOptionId
}