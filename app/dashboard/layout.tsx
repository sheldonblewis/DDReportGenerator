import SideNav from '../ui/dashboard/side-nav';

export default function Layout({ children }: { children: React.ReactNode }) {
      return (
      <main className="flex items-center justify-end bg-gray-100">
          <SideNav />
        <div className="flex w-10/12 flex-col p-4">
          <div className="grow p-6 md:overflow-y-auto md:p-12">{children}</div>
        </div>
      </main>
    );
  }