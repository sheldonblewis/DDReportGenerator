import EquitaryLogo from "@/app/ui/equitary-logo";
import { signOut } from "@/auth";
import Link from "next/link";

export default function SideNav() {
  return (
    <div className="flex h-screen flex-col justify-between border-e bg-white">
      <div className="px-4 py-6">
        <span className="grid h-10 w-32 place-content-center rounded-lg">
          <Link
            href="/dashboard"
            key="dashboard"
          >
            <EquitaryLogo />
          </Link>
        </span>
      </div>

      <div className="sticky inset-x-0 bottom-0 border-t border-gray-100">
        <div className="flex items-center gap-2 bg-white p-4 hover:bg-gray-50">
          <form
            action={async () => {
              "use server";
              await signOut();
            }}
          >
            <button className="mt-4 w-full text-black">Sign out</button>
          </form>
        </div>
      </div>
    </div>
  );
}
