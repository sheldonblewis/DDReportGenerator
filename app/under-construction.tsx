import SocialLinks from "./ui/global-components/social-links";
import MinimalHeader from "./ui/global-components/minimal-header";

export default function UnderConstruction() {
    return (
      <main className="bg-white flex justify-center items-center min-h-screen">
        <MinimalHeader />
        {/* Contact Page Landing - section */}
        <section className="max-w-[320px] text-center flex-nowrap justify-center items-center">
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Website is under construction</h1>
          <p className="text-slate-500 mt-4">Look out for updates on our socials</p>
          <SocialLinks/>
        </section>
      </main>
    );
  }