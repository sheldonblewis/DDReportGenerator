
import EquitaryIconLogo from "./equitary-icon"
export default function LoadingBar() {
    return (
        <div className="flex justify-center items-center flex-col gap-4">
            <EquitaryIconLogo />
            <div className="loader">
                <div className="bar"></div>
            </div>
        </div>
    )
}
