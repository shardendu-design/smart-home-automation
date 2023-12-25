import { assert } from "https://deno.land/std@0.202.0/testing/asserts.ts";
import { app } from "../app.js";
import { superoak } from "https://deno.land/x/superoak@4.7.0/mod.ts";

Deno.test("main page works", async () => {
  const testClient = await superoak(app);
  await testClient.get("localhost:7777/")
    .expect(new RegExp("Drill & Practice"));
})


  Deno.test("login works", async () => {
    const testClient = await superoak(app);
    await testClient.get("/auth/login")
      .expect(new RegExp("Login"));
  });

  Deno.test("register works", async () => {
    const testClient = await superoak(app);
    await testClient.get("/auth/register")
      .expect(new RegExp("Register"));
  });

  Deno.test("unauthorised visit to /quiz/:id", async () => {
    const testClient = await superoak(app);
    await testClient.get("/quiz/1")
      .expect(new RegExp("/auth/login"));
  });
  
  Deno.test("unauthorised visit to /topics/:id", async () => {
    const testClient = await superoak(app);
    await testClient.get("/topics/1")
      .expect(new RegExp("/auth/login"));
  });
  
  Deno.test("statistics exists", async () => {
    const testClient = await superoak(app);
    await testClient.get("/")
      .expect(new RegExp("Topics:"));
  });
  
  Deno.test("nav works for main page", async () => {
    const testClient = await superoak(app);
    await testClient.get("/")
      .expect(new RegExp("Topics"));
  });
  
  Deno.test("nav works for login form", async () => {
    const testClient = await superoak(app);
    await testClient.get("/auth/login")
      .expect(new RegExp("Quiz"));
  });
  
  Deno.test("/api/questions/random works", async () => {
    const testClient = await superoak(app);
    await testClient.get("/api/questions/random")
      .expect(200);
  });
  
  Deno.test("/api/questions/answer works", async () => {
    const testClient = await superoak(app);
    await testClient.post("/api/questions/answer")
      .send({ "questionId": 8, "optionId": 12 })
      .expect(200);
  });
  