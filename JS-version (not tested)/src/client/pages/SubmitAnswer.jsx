import React, { useState } from 'react';
import { useQuery } from '@wasp/queries';
import { useAction } from '@wasp/actions';
import getQuestion from '@wasp/queries/getQuestion';
import registerAnswer from '@wasp/actions/registerAnswer';

export function SubmitAnswer() {
  const [questionId, setQuestionId] = useState(0);
  const [answer, setAnswer] = useState('');
  const [proof, setProof] = useState(null);

  const { data: question } = useQuery(getQuestion, { id: questionId });
  const submitAnswer = useAction(registerAnswer);

  const handleQuestionChange = (e) => {
    setQuestionId(e.target.value);
  };

  const handleSubmit = () => {
    submitAnswer({ questionId, answer, proof });
  };

  return (
    <div className='p-4'>
      <div className='mb-4'>
        <label className='block mb-2 font-bold'>Question</label>
        <select className='border rounded p-2' value={questionId} onChange={handleQuestionChange}>
          <option value=''>-- Select a question --</option>
          {question && question.map((q) => (
            <option key={q.id} value={q.id}>{q.title}</option>
          ))}
        </select>
      </div>
      {question && (
        <div>
          <p>{question.title}</p>
          <div>
            <label className='block mb-2 font-bold'>Answer</label>
            <input
              type='text'
              className='border rounded p-2 mb-4'
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          </div>
          <div>
            <label className='block mb-2 font-bold'>Proof</label>
            <input
              type='file'
              className='border rounded p-2 mb-4'
              onChange={(e) => setProof(e.target.files[0])}
            />
          </div>
          <button
            onClick={handleSubmit}
            className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
          >
            Submit
          </button>
        </div>
      )}
    </div>
  );
}