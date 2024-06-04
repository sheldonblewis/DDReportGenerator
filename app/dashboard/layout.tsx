import SideNav from '../ui/dashboard/side-nav';

export default function Layout({ children }: { children: React.ReactNode }) {
      return (
      <main className="flex items-center justify-center h-screen bg-gray-100 border-b border-2 border-gray-300">
          <SideNav />
        <div className="flex w-full flex-col p-4">
          {/* <div className="flex h-20 w-full items-end rounded-lg bg-gray-200 p-3 md:h-36">
            <div className="w-32 text-black md:w-36">
              <Link
              href="/"
              key="home">
                  <span className='sr-only'>Go to home page</span>
                  <EquitaryLogo />
              </Link>
            </div>
          </div> */}
          <div className="grow p-6 md:overflow-y-auto md:p-12">{children}</div>
        </div>
      </main>
    );
  }