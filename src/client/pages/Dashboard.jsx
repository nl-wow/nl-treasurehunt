import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@wasp/queries';
import { useAction } from '@wasp/actions';
import getQuestion from '@wasp/queries/getQuestion';

export function Dashboard() {
  const { data: question, isLoading, error } = useQuery(getQuestion);

  if (isLoading) return 'Loading...';
  if (error) return 'Error: ' + error;

  const [answer, setAnswer] = useState('');

  const handleAnswerSubmit = () => {
    // Submit the answer
  };

  return (
    <div className='p-4'>
      <h1 className='text-3xl font-bold mb-4'>Dashboard</h1>
      <div className='mb-4'>
        <h2 className='text-2xl font-bold mb-2'>{question.title}</h2>
        <p>{question.description}</p>
      </div>
      <div className='mb-4'>
        <input
          type='text'
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className='px-4 py-2 border rounded'
        />
      </div>
      <div>
        <button
          onClick={handleAnswerSubmit}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
        >
          Submit Answer
        </button>
      </div>
      <div>
        <Link to='/leaderboard' className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-2'>
          Leaderboard
        </Link>
      </div>
    </div>
  );
}