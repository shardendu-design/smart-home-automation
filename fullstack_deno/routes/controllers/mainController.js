import * as topicService from "../../services/topicService.js";
import * as questionService from "../../services/questionService.js";
import * as questionAnswerService from "../../services/questionAnswerService.js";
import * as awairrowdataService from "../../services/awairrowdataService";
const showMain = async ({ render }) => {
  const statData = {
    topics: 0,
    questions: 0,
    answers: 0,
  };

  const data = {
      awairRow: await awairrowdataService.findAll(),
  };
  // return new Response(await renderFile("main.eta", data), responseDetails);


  statData.topics = await topicService.getTopicsCount();
  statData.questions = await questionService.getQuestionCount();
  statData.answers = await questionAnswerService.getQuestionAnswersCount();
  
  

  render("main.eta", { topics: statData.topics, questions: statData.questions, answers: statData.answers });
};

export { showMain };