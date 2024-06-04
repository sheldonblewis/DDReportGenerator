import { useState } from 'react';
import SocialLinks from "./ui/global-components/social-links";
import MinimalHeader from "./ui/global-components/minimal-header";

export default function UnderConstruction() {
  const [password, setPassword] = useState("");
  const correctPassword = "YourCorrectPassword"; // replace with the actual correct password

  const handlePasswordChange = (e:any) => {
    setPassword(e.target.value);
  };

  const handleGoClick = () => {
    if (password === correctPassword) {
      window.location.href = 'document-upload'; // Navigate to the document upload page
    } else {
      alert("Incorrect password");
    }
  };

  return (
    <main className="bg-white flex justify-center items-center min-h-screen">
      <MinimalHeader />
      {/* Contact Page Landing - section */}
      <section className="max-w-[320px] text-center flex-nowrap justify-center items-center">
        <h1 className="text-2xl font-bold tracking-tight text-black sm:text-3xl">Website is under construction</h1>
        <p className="text-black mt-4">Look out for updates on our socials</p>
        <SocialLinks />
        <div className="mt-6">
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            placeholder="Enter password"
            className="border border-gray-300 p-2 rounded text-black"
          />
          <button
            onClick={handleGoClick}
            className="ml-2 p-2 bg-blue-500 text-white rounded"
          >
            Go
          </button>
        </div>
      </section>
    </main>
  );
}
