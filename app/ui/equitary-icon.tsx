import Image from 'next/image'

export default function EquitaryIconLogo() {
  return (
    <div className="">
      <Image
        src="/Equitary-icon-logo.svg"
        width={50}
        height={40}
        alt="Equitary logo"
      />
      {/* <p className="text-[44px] ">Acme</p> */}
    </div>
  );
}