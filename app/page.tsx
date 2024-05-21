"use client";
import Image from "next/image";
import { inter } from '@/app/ui/fonts';
import { useState } from 'react'
import { Dialog } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import EquitaryLogo from '@/app/ui/equitary-logo';
import { ShieldCheckIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Header from "@/app/ui/global-components/header";
import Footer from "@/app/ui/global-components/footer";

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  return (
    <main>
      {/* Home Page Landing - section */}
      <section className="bg-gray-100 border-b border-2 border-gray-300 min-h-screen">
        <Header />

        <div className="relative isolate px-6 pt-14 lg:px-8">
          {/* <div
            className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
            aria-hidden="true"
          >
            <div
              className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
              style={{
                clipPath:
                  'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
              }}
            />
          </div> */}
          <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
            {/* <div className="hidden sm:mb-8 sm:flex sm:justify-center">
              <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
                Announcing our next round of funding.{' '}
                <a href="#" className="font-semibold text-indigo-600">
                  <span className="absolute inset-0" aria-hidden="true" />
                  Read more <span aria-hidden="true">&rarr;</span>
                </a>
              </div>
            </div> */}
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Due Dillegence Reports<br />AI Powered
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Itaque necessitatibus et tempora, distinctio aspernatur magni voluptates.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <a
                  href="#"
                  className="rounded-md bg-equitaryPrimary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Sign Up - Get Access
                </a>
                {/* <a href="#" className="text-sm font-semibold leading-6 text-gray-900">
                  Learn more <span aria-hidden="true">→</span>
                </a> */}
              </div>
            </div>
          </div>
          {/* <div
            className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
            aria-hidden="true"
          >
            <div
              className="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
              style={{
                clipPath:
                  'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
              }}
            />
          </div> */}
        </div>
      </section>
      {/* Working With Equitary - section */}
      <section className="bg-gray-100 border-b border-2 border-gray-300 p-16">
        <div className="text-black ml-12 mb-12">
          <h2 className="text-2xl font-semibold mb-4">Working with Equitary</h2>
          <p className="mb-2">Equitary is easy to use</p>
          <ol className="list-decimal list-inside">
            <li>Import a set of files</li>
            <li>Wait up to only 4 minutes</li>
            <li>Access a thorough report with details and alerts</li>
          </ol>
        </div>
        {/* Cards */}
        <div className="grid grid-cols-2 gap-12 px-12">
          {/* Card One */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
          {/* Card Two */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
          {/* Card Three */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
        </div>
      </section>
      {/* Security is key - section */}
      <section className="bg-gray-200 border-b border-2 border-gray-300 min-h-screen flex-nowrap justify-center p-16">
        <div className="flex justify-center mb-16">
          <h2 className="flex items-center text-2xl font-semibold text-black">
            <ShieldCheckIcon className="h-12 w-12 text-black"/>
            &nbsp; Security is Key
          </h2>
        </div>
        {/* Cards */}
        <div className="grid grid-cols-3 gap-12 px-12">
          {/* Card One */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
          {/* Card Two */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
          {/* Card Three */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
            </div>
        </div>
      </section>
      {/* Equitary is Proven and Trusted - section */}
      <section className="bg-gray-100 border-b border-2 border-gray-300 min-h-screen flex-nowrap justify-center p-16">
        <div className="flex justify-center mb-16">
          <h2 className="flex items-center text-2xl font-semibold text-black">
            {/* <ShieldCheckIcon className="h-12 w-12 text-black"/> */}
            &nbsp; Equitary is Proven and Trusted
          </h2>
        </div>
        {/* Cards */}
        <div className="grid grid-cols-4 gap-12 px-12">
          {/* Card One */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
          </div>
          {/* Card Two */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
          </div>
          {/* Card Three */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
          </div>
          {/* Card Four */}
          <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96">
              <div className="mb-8">
                <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
              </div>
              {/* <div className="flex items-center">
                <div className="text-sm">
                  <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                  <p className="text-gray-600">Aug 18</p>
                </div>
              </div> */}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
