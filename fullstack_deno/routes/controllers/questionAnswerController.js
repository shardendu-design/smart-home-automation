import { validasaur } from "../../deps.js";
import * as questionService from "../../services/questionService.js";
import * as questionAnswerService from "../../services/questionAnswerService.js";

const answerValidationRules = {
    optionText: [validasaur.required, validasaur.minLength(1)],
}

const deleteAnswerOption = async ({ response, params }) => {
    const questionID = params.questionId
    const optionId = params.optionId
    await questionAnswerService.deleteAnswerByOptionId(optionId)
    await questionAnswerService.deleteAnswerOption(questionID, optionId)
    response.redirect(`/topics/${params.tid}/questions/${questionID}`)
}

const addAnswerOptions = async ({ request, response, render, params, state }) => {
    try {
        const id = params.id;
        const body = request.body({ type: "form" });
        const data = await body.value;
        const answerOptionData = {
            optionText: data.get("option_text"),
            isCorrect: data.get("is_correct"),
        };
        const [passes, errors] = await validasaur.validate(
            answerOptionData,
            answerValidationRules,
        );
        const questionData = await questionService.getQuestionByQuestionID(id);

        const userId = (await state.session.get("user")).id;
        if (parseInt(userId) !== parseInt(questionData[0].user_id)) {
            response.body = "You cannot post an option to others' question";
            return;
        }

        if (!passes) {
            questionData.validationErrors = errors;
            questionData.optionText = answerOptionData.optionText;
            questionData.details = await questionAnswerService.getAnswerByQuestionId(id);
            questionData.topicId = params.tid;
            render("question.eta", questionData);
        } else {
            const isCorrect = answerOptionData.isCorrect === "on";
            await questionAnswerService.addAnswerOptions(id, answerOptionData.optionText, isCorrect);
            response.redirect(`/topics/${params.tid}/questions/${id}`);
        }
    } catch (error) {
        console.error("Error processing request:", error);  
        response.body = "An error occurred while processing your request";
    }
};


export { addAnswerOptions, deleteAnswerOption }