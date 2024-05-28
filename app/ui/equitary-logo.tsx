import Image from 'next/image'

export default function EquitaryLogo() {
  return (
    <div className="flex flex-row items-center leading-none text-white">
      <Image
        src="/Equitary-logo-large.svg"
        width={125}
        height={42}
        alt="Equitary logo, button, home page"
      />
      {/* <p className="text-[44px] ">Acme</p> */}
    </div>
  );
}