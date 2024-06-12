import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import { Suspense } from 'react';
import {
  RevenueChartSkeleton
} from '@/app/ui/skeletons';

export default async function Page() {
  return (
    <main>
      <h1 className={`mb-4 text-xl md:text-2xl text-black`}>
        Report
      </h1>
      <div className="mt-6 grid grid-cols-1">
        <Suspense fallback={<RevenueChartSkeleton />}>
          <RevenueChart />
        </Suspense>
      </div>
    </main>
  );
}