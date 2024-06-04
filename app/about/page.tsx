import Header from "@/app/ui/global-components/header";
import Footer from "@/app/ui/global-components/footer";
import Image from "next/image";
import { inter } from '@/app/ui/fonts';
import { useState } from 'react'
import { Dialog } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import EquitaryLogo from '@/app/ui/equitary-logo';
import { ShieldCheckIcon } from "@heroicons/react/24/outline";
import Link from "next/link";

export default function Page() {
    return (
      <main>
        {/* About Page Landing - section */}
        <section className="bg-gray-100 border-b border-2 border-gray-300">
          <Header />

          <div className="relative isolate px-6 pt-14 lg:px-8">
            <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
              <div className="text-center">
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                  About Equitary
                </h1>
                <p className="mt-6 text-lg leading-8 text-gray-600">
                  What is Equitary, who is Equitary?
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* What do we do at Equitary? - section */}
        <section className="bg-gray-100 border-b border-2 border-gray-300 p-16">
          {/* Section Description & Card */}
          <div className="grid grid-cols-3 gap-12 px-12">
            {/* Card One */}
            <div className="text-black ml-12 mb-12 col-span-1">
              <h2 className="text-2xl font-semibold mb-4">What do we do at Equitary?</h2>
            </div>
            
            <div className="p-4 leading-normal h-96 col-span-2">
              <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Elementum nisi quis eleifend quam adipiscing. Sagittis orci a scelerisque purus. Posuere ac ut consequat semper viverra. Arcu bibendum at varius vel pharetra vel turpis nunc. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Elementum nisi quis eleifend quam adipiscing. Sagittis orci a scelerisque purus. Posuere ac ut consequat semper viverra. Arcu bibendum at varius vel pharetra vel turpis nunc.</p>
            </div>
          </div>
        </section>

        {/* Background - section */}
        <section className="bg-gray-200 border-b border-2 border-gray-300 min-h-screen flex-nowrap justify-center p-16">
          {/* Section Description & Card */}
          <div className="grid grid-cols-3 gap-12 px-12">
            {/* Card One */}
            <div className="text-black ml-12 mb-12 col-span-1">
              <h2 className="text-2xl font-semibold mb-4">Background</h2>
            </div>
            {/* Card Tile */}
            <div className="col-span-2">
              <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
                  <div className="mb-8">
                    <div className="text-gray-900 font-bold text-xl mb-2">Card heading</div>
                    <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
                  </div>
              </div>
              <p className="text-gray-700 text-base mt-8">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-12 px-12 mt-32">
            {/* Card One */}
            <div className="text-black ml-12 mb-12 col-span-1">
              <h2 className="text-2xl font-semibold mb-4">Founders</h2>
            </div>
            {/* Founder tile 1 */}
            <div className="col-span-1">
              <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
                  <div className="mb-8">
                  </div>
              </div>
              <p className="text-gray-900 font-bold text-xl mb-2 text-center mt-8">Name #1</p>
            </div>
            {/* Founder Tile 2 */}
            <div className="col-span-1">
              <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
                  <div className="mb-8">
                  </div>
              </div>
              <p className="text-gray-900 font-bold text-xl mb-2 text-center mt-8">Name #2</p>
            </div>
          </div>
        </section>

        <Footer />
      </main>
    );
  }