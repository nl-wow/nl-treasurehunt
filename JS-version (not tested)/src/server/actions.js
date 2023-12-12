import HttpError from '@wasp/core/HttpError.js'

export const publishQuestion = async (args, context) => {
  if (!context.user || !context.user.isAdmin) { throw new HttpError(401) }

  return context.entities.Question.update({
    where: { id: args.questionId },
    data: { published: true }
  });
}

export const registerAnswer = async (args, context) => {
  if (!context.user) { throw new HttpError(401) };

  const { questionId, answer, proof } = args;

  const question = await context.entities.Question.findUnique({
    where: { id: questionId }
  });

  if (!question) { throw new HttpError(404) };

  const isCorrect = question.answers.some(a => a.content === answer);

  const createdAnswer = await context.entities.Answer.create({
    data: {
      content: answer,
      proof: proof,
      isCorrect: isCorrect,
      question: { connect: { id: questionId } },
      user: { connect: { id: context.user.id } }
    }
  });

  return createdAnswer;
}

export const checkAnswer = async (args, context) => {
  if (!context.user) { throw new HttpError(401) };

  const answer = await context.entities.Answer.findUnique({
    where: { id: args.id }
  });
  if (answer.isCorrect) { throw new HttpError(403) };

  return context.entities.Answer.update({
    where: { id: args.id },
    data: { isCorrect: true }
  });
}