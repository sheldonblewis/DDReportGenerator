"use client";
import Image from "next/image";
import { useState } from 'react'
import { ShieldCheckIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Header from "@/app/ui/global-components/header";
import Footer from "@/app/ui/global-components/footer";
import UnderConstruction from "./under-construction";
import { IsUnderConstruction } from '@/app/lib/definitions';
import axios from 'axios';

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  
  const [files, setFiles] = useState({
    balSheet: null,
    incStatement: null,
    cfStatement: null,
    cimFile: null,
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFiles(e.target.files);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selectedFiles) return;

    const formData = new FormData();
    Array.from(selectedFiles).forEach((file, index) => {
      formData.append(file.name, file);
    });

    try {
      const response = await axios.post('http://localhost:9998', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File upload response:', response.data);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  return (
    <main>
      {/* Home Page Landing - section */}
      <section className="bg-gray-100 border-b border-2 border-gray-300 min-h-screen">
        <Header />
        <div className="relative isolate px-6 pt-14 lg:px-8">
          <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Due Diligence Reports
                <br />
                AI Powered
              </h1>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Itaque
                necessitatibus et tempora, distinctio aspernatur magni
                voluptates.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link
                  key="register"
                  href="/register"
                  className="rounded-md bg-equitaryPrimary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Sign Up - Get Access
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* File Upload Section */}
      <section className="bg-gray-100 border-b border-2 border-gray-300 p-16">
        <div className="text-black ml-12 mb-12">
          <h2 className="text-2xl font-semibold mb-4">Upload Files</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="balSheet">Balance Sheet:</label>
              <input
                type="file"
                name="balSheet"
                onChange={handleFileChange}
                required
              />
            </div>
            <div>
              <label htmlFor="incStatement">Income Statement:</label>
              <input
                type="file"
                name="incStatement"
                onChange={handleFileChange}
                required
              />
            </div>
            <div>
              <label htmlFor="cfStatement">Cash Flow Statement:</label>
              <input
                type="file"
                name="cfStatement"
                onChange={handleFileChange}
                required
              />
            </div>
            <div>
              <label htmlFor="cimFile">CIM File:</label>
              <input
                type="file"
                name="cimFile"
                onChange={handleFileChange}
                required
              />
            </div>
            <button
              type="submit"
              className="rounded-md bg-equitaryPrimary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-equitaryPrimaryHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Create Job
            </button>
          </form>
        </div>
      </section>

      <Footer />
    </main>
  );
}
