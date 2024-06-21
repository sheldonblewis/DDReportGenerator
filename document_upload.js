// Import fetch at the top of your file
import fetch from 'wix-fetch';
import wixLocation from 'wix-location';

$w.onReady(function () {
    $w("#html1").src = "https://equitary-uploads.ngrok.io/";

    $w("#html1").onMessage((event) => {
        if (event.data.status === "uploadStarted") {
            console.log("Upload has started.");
        } else if (event.data.status === "uploadCompleted") {
            console.log("Upload has completed.");
            checkForUploadCompletion();
        }
    });
});

function checkForUploadCompletion() {
    const pollingInterval = 1000;
    const checkEndpoint = "https://equitary-uploads.ngrok.io/get-latest-report";

    const intervalId = setInterval(() => {
        fetch(checkEndpoint, { method: 'get' })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.log("Polling for completion, but data is not ready yet.");
                } else {
                    console.log("Data received:", data);
                    clearInterval(intervalId); // Stop polling
                    updateHtmlComponent(data);
                }
            })
            .catch(err => {
                console.error("Error polling for upload completion:", err);
                clearInterval(intervalId);
            });
    }, pollingInterval);
}

function updateHtmlComponent(data) {
    // Trim and encode the financial statements and CIM report
    const encodedIncomeStatement = encodeURIComponent(data.incStatement.trim());
    const encodedBalanceSheet = encodeURIComponent(data.balSheet.trim());
    const encodedCfStatement = encodeURIComponent(data.cfStatement.trim());
    const encodedCimFile = encodeURIComponent(data.cimFile.trim());

    if (data.incStatement && data.balSheet && data.cfStatement && data.cimFile) {
        wixLocation.to(`/due-diligence-report?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}&cim_file=${encodedCimFile}`);
    }
}
