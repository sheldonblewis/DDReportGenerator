"use client";
import Image from "next/image";
import { inter } from '@/app/ui/fonts';
import { useState } from 'react'
import { Dialog } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import EquitaryLogo from '@/app/ui/equitary-logo';
import { ShieldCheckIcon } from "@heroicons/react/24/outline";
import Link from "next/link";

const navigation = [
    { name: 'About', href: '/about' },
    { name: 'Community', href: '#' },
    { name: 'Contact', href: '#' },
    { name: 'Pricing', href: '#' },
  ]

export default function Footer() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  return (
     
    <footer className="bg-white">
    <div className="mx-auto max-w-screen-xl space-y-8 px-4 py-16 sm:px-6 lg:space-y-16 lg:px-8">
      <div className="flex justify-between">
        <div>
          <div className="">
            <a href="#" className="">
              <span className="sr-only">Equitary</span>
              <EquitaryLogo/>
            </a>
          </div>

          {/* <p className="mt-4 max-w-xs text-gray-500">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Esse non cupiditate quae nam
            molestias.
          </p> */}

          <ul className="mt-8 flex gap-6">

            <li>
              <a
                href="https://twitter.com/equitaryinc"
                rel="noreferrer"
                target="_blank"
                className="text-gray-700 transition hover:opacity-75"
              >
                <span className="sr-only">X (formarly Twitter)</span>

                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"
                  />
                </svg>
              </a>
            </li>

            <li>
              <a
                href="https://www.linkedin.com/company/equitary"
                rel="noreferrer"
                target="_blank"
                className="text-gray-700 transition hover:opacity-75"
              >
                <span className="sr-only">LinkedIn</span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" strokeWidth="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
              </a>
            </li>

            <li>
              <a
                href="https://www.instagram.com/equitary/"
                rel="noreferrer"
                target="_blank"
                className="text-gray-700 transition hover:opacity-75"
              >
                <span className="sr-only">Instagram</span>

                
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    fill-rule="evenodd"
                    d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z"
                    clip-rule="evenodd"
                  />
                </svg>
              </a>
            </li>
          </ul>
        </div>

        {/* <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:col-span-2 lg:grid-cols-4"> */}
          {/* Services */}
          {/* <div>
            <p className="font-medium text-gray-900">Services</p>

            <ul className="mt-6 space-y-4 text-sm">
              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> 1on1 Coaching </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Company Review </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Accounts Review </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> HR Consulting </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> SEO Optimisation </a>
              </li>
            </ul>
          </div> */}
          {/* Company */}
          {/* <div>
            <p className="font-medium text-gray-900">Company</p>

            <ul className="mt-6 space-y-4 text-sm">
              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> About </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Meet the Team </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Accounts Review </a>
              </li>
            </ul>
          </div> */}
          {/* Helpful Links */}
          {/* <div>
            <p className="font-medium text-gray-900">Helpful Links</p>

            <ul className="mt-6 space-y-4 text-sm">
              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Contact </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> FAQs </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Live Chat </a>
              </li>
            </ul>
          </div> */}
          {/* Legal */}
          {/* <div>
            <p className="font-medium text-gray-900">Legal</p>

            <ul className="mt-6 space-y-4 text-sm">
              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Accessibility </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Returns Policy </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Refund Policy </a>
              </li>

              <li>
                <a href="#" className="text-gray-700 transition hover:opacity-75"> Hiring Statistics </a>
              </li>
            </ul>
          </div> */}
        {/* </div> */}
         {/* Card One */}
        <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal w-1/2">
            <div className="">
              <div className="text-gray-900 font-bold text-l mb-2">Join the Equitary Community</div>
              <p className="text-gray-700 text-base">Receive updates and news from us at Equitary</p>
            </div>
            {/* <div className="flex items-center">
              <div className="text-sm">
                <p className="text-gray-900 leading-none">Jonathan Reinink</p>
                <p className="text-gray-600">Aug 18</p>
              </div>
            </div> */}
            <div className="flex gap-8 mt-2">
              <div className="w-2/3">
                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                  <span className="sr-only">Email address</span>
                </label>
                <div className="">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    placeholder="Email"
                    className="block w-full rounded-md border-0 p-2.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
                <a
                href="#"
                className="w-1/3 rounded-md bg-equitaryPrimary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Sign Up - Get Access
              </a>
            </div>
            
        </div>
      </div>

      {/* <p className="text-xs text-gray-500">&copy; 2022. Company Name. All rights reserved.</p> */}
    </div>
  </footer>
  );
}