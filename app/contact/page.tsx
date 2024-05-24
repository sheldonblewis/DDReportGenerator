
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
      <main className="bg-gray-100 ">
        {/* Contact Page Landing - section */}
        <section className="bg-gray-100 border-b border-2 border-gray-300">
          <Header />

          <div className="relative isolate px-6 pt-14 lg:px-8">
            <div className="mx-auto max-w-2xl mt-[180px]">
              <div className="text-center">
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                  Get in Touch
                </h1>
                <p className="mt-6 text-lg leading-8 text-gray-600">
                    Have a question? Any kind of inquires are welcome.
                </p>
              </div>
            </div>
          </div>
          <div className="flex-nowrap justify-center px-16 pb-16">
            <div className="grid grid-cols-3 gap-12 px-12 mt-32">
                {/* Founder tile 1 */}
                <div className="col-span-1 text-center">
                    <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
                        <div className="mb-8">
                            <div className="text-gray-900 font-bold text-xl mb-2">How do I get access?</div>
                            <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi atque non dolore. Inventore blanditiis eius accusamus odit sequi debitis nesciunt architecto nemo quisquam, voluptatem veniam harum laborum deserunt quia voluptatum?
                            Ipsam minima iste ducimus accusantium minus maxime quae perferendis assumenda. Quis, animi, blanditiis neque ipsa, maxime alias nisi libero inventore corrupti nemo quam officia explicabo. Eaque dolor at voluptatibus numquam?</p>
                        </div>
                    </div>
                </div>
                {/* Founder tile 1 */}
                <div className="col-span-1 text-center">
                    <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-4 flex flex-col justify-center leading-normal h-96 col-span-2">
                        <div className="mb-8">
                            <div className="text-gray-900 font-bold text-xl mb-2">How does it work?</div>
                            <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis et eius qui molestias quia eligendi impedit explicabo expedita voluptatem, laboriosam ducimus tempora? Ad expedita aliquid distinctio qui molestias. Doloremque, rerum!
                            Explicabo sunt reiciendis ipsam nemo. Eos, nobis quis ducimus et suscipit dolore fugiat sequi nulla odio dolorem repellat aperiam voluptas dicta praesentium sunt recusandae perferendis? Maiores fugit reiciendis molestias dolore.</p>
                        </div>
                    </div>
                </div>
                {/* Founder Tile 2 */}
                <div className="col-span-1 text-center">
                    <div className="border border-gray-400 lg:border lg:border-gray-400 bg-gray-300 rounded-lg p-8 flex flex-col justify-center leading-normal min-h-96 col-span-2">
                        <div className="mb-8">
                            <div className="text-gray-900 font-bold text-xl mb-2">General inquiries</div>
                            <p className="text-gray-700 text-base">Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas optio culpa a nisi mollitia fugiat sint reprehenderit dolor ipsam non, itaque ullam amet? Natus, quam porro sint suscipit aperiam ea.
                            Obcaecati quos dignissimos natus quisquam deserunt ex mollitia adipisci rem doloribus deleniti, fugiat impedit sint delectus cupiditate quis consectetur quas commodi laboriosam ipsam maiores distinctio nisi necessitatibus consequuntur! Eius, corporis!</p>
                        </div>
                    </div>
                </div>
            </div>
          </div>
        </section>

        <section className="bg-gray-100 p-16 mx-auto w-1/2">
        <form>
        <div className="pb-12">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Contact Us</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">Reach out to us with any questions you have</p>

          <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div className="sm:col-span-3">
              <label htmlFor="first-name" className="block text-sm font-medium leading-6 text-gray-900">
                <span className="sr-only">First name</span>
              </label>
              <div className="mt-2">
                <input
                  placeholder="First name"
                  type="text"
                  name="first-name"
                  id="first-name"
                  autoComplete="given-name"
                  className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div className="sm:col-span-3">
              <label htmlFor="last-name" className="block text-sm font-medium leading-6 text-gray-900">
                <span className="sr-only">Last name</span>
              </label>
              <div className="mt-2">
                <input
                  placeholder="Last name"
                  type="text"
                  name="last-name"
                  id="last-name"
                  autoComplete="family-name"
                  className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div className="sm:col-span-4">
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                <span className="sr-only">Email address</span>
              </label>
              <div className="mt-2">
                <input
                  placeholder="Email address"
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div className="sm:col-span-4">
              <label htmlFor="company" className="block text-sm font-medium leading-6 text-gray-900">
                <span className="sr-only">Company</span>
              </label>
              <div className="mt-2">
                <input
                  placeholder="Company"
                  id="company"
                  name="company"
                  type="text"
                  autoComplete="organization"
                  className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div className="sm:col-span-6">
              <label htmlFor="message" className="block text-sm font-medium leading-6 text-gray-900">
                <span className="sr-only">Message</span>
              </label>
              <div className="mt-2">
                <textarea
                    id="message"
                    className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    placeholder="Message"
                ></textarea>
              </div>
            </div>

            <div className="sm:col-span-6 place-self-end">
            <button
                className="rounded-md bg-equitaryPrimary px-12 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
                Send
            </button>
            </div>
          </div>
        </div>
        </form>

        </section>
        <Footer />
      </main>
    );
  }