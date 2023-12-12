import HttpError from '@wasp/core/HttpError.js'

export const getQuestion = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  const question = await context.entities.Question.findUnique({
    where: { id: args.id },
    include: { answers: true }
  });

  if (!question) throw new HttpError(400);

  return question;
}

export const getAnswer = async (args, context) => {
  if (!context.user) { throw new HttpError(401) }

  const answer = await context.entities.Answer.findUnique({
    where: { id: args.id },
  });

  if (!answer) { throw new HttpError(400) }

  return answer;
}

export const getAnswers = async (args, context) => {
  if (!context.user || !context.user.isAdmin) { throw new HttpError(401) };

  return context.entities.Answer.findMany();
}