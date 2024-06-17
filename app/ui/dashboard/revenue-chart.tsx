'use client';
import { generateYAxis } from '@/app/lib/utils';
// import { CalendarIcon } from '@heroicons/react/24/outline';
// import "chart.js/auto";
// import {Bar} from 'react-chartjs-2'
// import { fetchRevenue } from '@/app/lib/data';

// Fake Data
// const revenue = [
//     { month: 'Jan', revenue: 2000 },
//     { month: 'Feb', revenue: 1800 },
//     { month: 'Mar', revenue: 2200 },
//     { month: 'Apr', revenue: 2500 },
//     { month: 'May', revenue: 2300 },
//     { month: 'Jun', revenue: 3200 },
//     { month: 'Jul', revenue: 3500 },
//     { month: 'Aug', revenue: 3700 },
//     { month: 'Sep', revenue: 2500 },
//     { month: 'Oct', revenue: 2800 },
//     { month: 'Nov', revenue: 3000 },
//     { month: 'Dec', revenue: 4800 },
//   ];
  
// const chartData = {
//     labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//     datasets: [
//         {
//             label: 'Revenue',
//             barThickness: 10,
//             borderRadius: 30,
//             backgroundColor: 'rgba(47, 97, 68, 0.3)',
//             data: [2000, 1800, 2200, 2500, 2300, 3200, 3500, 3700, 2500, 2800, 6000, 8200]
//         }
//     ]
// }

// const options = {
//     plugins: {
//         legend: {
//             position: "top",
//             align: "start",
//             labels: {
//                 boxWidth: 7,
//                 usePointStyle: true,
//                 pointStyle: "circle",
//             },
//             title: {
//                 text: "Sales Report",
//                 display: true,
//                 color: "4000",
//                 font: {
//                     size: 18,
//                 },
//             },
//         },
//     },
//     scales: {
//         xAxis: {
//             display: false,
//         },
//         yAxis: {
//             max: 1,
//         },
//     },
//     elements: {
//         bar: {
//             barPercentage: 0.3,
//             categoryPercentage: 1,
//         },
//     },
// };


export default async function RevenueChart() {
//   const revenue = await fetchRevenue();

  const chartHeight = 350;
//   const { yAxisLabels, topLabel } = generateYAxis(revenue);


//   if (!revenue || revenue.length === 0) {
//     return <p className="mt-4 text-gray-400">No data available.</p>;
//   }

  return (
    <div className="w-full md:col-span-4">
      <h2 className="mb-4 text-xl md:text-2xl text-black">
        Due Dillegence Report
      </h2>
      <div className="rounded-xl bg-gray-50 p-4">
        {/* <Bar data={chartData} height={300} ></Bar> */}
        <span>report download goes here</span>
        {/* <div className="mt-0 grid grid-cols-13 items-end gap-2 rounded-md bg-white p-4 sm:grid-cols-13 md:gap-4">
          <div
            className="mb-6 hidden flex-col justify-between text-sm text-gray-400 sm:flex"
            style={{ height: `${chartHeight}px` }}
          >
            {yAxisLabels.map((label) => (
              <p key={label}>{label}</p>
            ))}
          </div>

          {revenue.map((month) => (
            <div key={month.month} className="flex flex-col items-center gap-2">
              <div
                className="w-full rounded-md bg-blue-300"
                style={{
                  height: `${(chartHeight / topLabel) * month.revenue}px`,
                }}
              ></div>
              <p className="-rotate-90 text-sm text-gray-400 sm:rotate-0">
                {month.month}
              </p>
            </div>
          ))}
        </div> */}
        {/* <div id="chart"></div>
        <div className="flex items-center pb-2 pt-6">
          <CalendarIcon className="h-5 w-5 text-gray-500" />
          <h3 className="ml-2 text-sm text-gray-500 ">Last 12 months</h3>
        </div> */}
      </div>
    </div>
  );
}