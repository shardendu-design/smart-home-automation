import * as questionService from "../../services/questionService.js";
import * as questionAnswerService from "../../services/questionAnswerService.js";


const getRandomQuestion = async ({ response }) => {
    try {
        const randomQuestion = await questionService.getRandomQuestionAPI();

        if (randomQuestion !== null) {
            const questionId = randomQuestion.id;
            const optionsData = await questionAnswerService.getAnswerByQuestionId(questionId);

            const formattedOptionsData = optionsData.map(option => ({
                optionId: option.id,
                optionText: option.option_text,
            }));

            const data = {
                questionId: randomQuestion.id,
                questionTitle: randomQuestion.title,
                questionText: randomQuestion.question_text,
                answerOptions: formattedOptionsData,
            };

            response.body = data;
        } else {
            response.body = {};
        }
    } catch (error) {
        console.error("Error fetching random question:", error);
        response.status = 500; 
        response.body = { error: "An error occurred while fetching the question." };
    }
};


const processAnswer = async ({ request, response }) => {
    const body = request.body()
    const content = await body.value
    const questionId = content.questionId
    const optionId = content.optionId
    const correctOptionIds = []
    const res = await questionAnswerService.getCorrectOption(questionId)
    if (res.length > 0) {
        for (let i = 0; i < res.length; i++) {
            correctOptionIds.push(res[i].id)
        }
        const isCorrect = correctOptionIds.includes(Number(optionId))
        const responseData = {
            correct: isCorrect,
        }
        response.body = responseData
    } else {
        response.body = {}
    }
}

export { getRandomQuestion, processAnswer }