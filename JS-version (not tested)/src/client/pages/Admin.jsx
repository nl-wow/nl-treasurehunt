import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@wasp/queries';
import { useAction } from '@wasp/actions';
import getQuestion from '@wasp/queries/getQuestion';
import registerAnswer from '@wasp/actions/registerAnswer';
import checkAnswer from '@wasp/actions/checkAnswer';
import publishQuestion from '@wasp/actions/publishQuestion';

export function Admin() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [proof, setProof] = useState('');

  const handlePublishQuestion = () => {
    publishQuestion({ question });
    setQuestion('');
  };

  const handleRegisterAnswer = () => {
    registerAnswer({ answer, proof });
    setAnswer('');
    setProof('');
  };

  const handleCheckAnswer = () => {
    checkAnswer({ answer });
    setAnswer('');
  };

  return (
    <div className='p-4'>
      <h1 className='text-2xl font-bold mb-4'>Admin Panel</h1>

      <div className='mb-4'>
        <h2 className='text-lg font-bold'>Publish Question</h2>
        <input
          type='text'
          placeholder='Question'
          className='px-1 py-2 border rounded mb-2'
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          onClick={handlePublishQuestion}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Publish
        </button>
      </div>

      <div className='mb-4'>
        <h2 className='text-lg font-bold'>Register Answer</h2>
        <input
          type='text'
          placeholder='Answer'
          className='px-1 py-2 border rounded mb-2'
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />
        <input
          type='text'
          placeholder='Proof'
          className='px-1 py-2 border rounded mb-2'
          value={proof}
          onChange={(e) => setProof(e.target.value)}
        />
        <button
          onClick={handleRegisterAnswer}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Register
        </button>
      </div>

      <div className='mb-4'>
        <h2 className='text-lg font-bold'>Check Answer</h2>
        <input
          type='text'
          placeholder='Answer'
          className='px-1 py-2 border rounded mb-2'
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />
        <button
          onClick={handleCheckAnswer}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Check
        </button>
      </div>

      <div>
        <h2 className='text-lg font-bold'>Leaderboard</h2>
        <Link to='/leaderboard' className='text-blue-500 hover:underline'>Go to Leaderboard</Link>
      </div>
    </div>
  );
}