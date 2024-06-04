import { Suspense } from 'react';
import { randomUUID } from 'crypto';
import Link from 'next/link';

export default function Dashboard() {
    let id = randomUUID();
    return (
      <main className="flex items-center justify-center md:h-screen bg-gray-100 border-b border-2 border-gray-300">
        <div className="relative mx-auto flex w-full max-w-[600px] flex-col space-y-2.5 p-4 md:-mt-32 text-black">
          
          <h1>Hello Customer</h1>
          <p>Welcome to your dashboard</p>
          <Link className='rounded-md bg-equitaryPrimary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
            href={`/dashboard/jobs/${id}`}
            key={id}
          >
            New Job
          </Link>
        </div>
      </main>
    );
  }