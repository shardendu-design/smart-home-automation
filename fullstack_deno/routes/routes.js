import { Router } from "../deps.js";
import * as mainController from "./controllers/mainController.js";
import * as userController from "./controllers/userController.js";

const router = new Router();

router.get("/", mainController.showMain);

router.get("/auth/register", userController.showRegistrationForm);
router.post("/auth/register", userController.postRegistrationForm);
router.get("/auth/login", userController.showLoginForm);
router.post("/auth/login", userController.postLoginForm);

export { router };
