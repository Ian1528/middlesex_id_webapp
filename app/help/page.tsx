export default function Page(){
    return (
        <div className="flex flex-col items-center m-auto p-10">
            <h1 className="text-lg font-bold p-10">Instructions</h1>
            <ul className="list-disc gap-3">
                <li>Choose the minimum number of words (or lines, in the case of Hamlet), for the ID</li>
                <li>Choose whether or not to hide the names of important characters using the toggle switch</li>
                <li>To check your answers, use Ctrl+F in the PDF or text file box.</li>
                <li>For books not listed, you must upload a text file. For best results, the text file should have newlines between paragraphs.
                    To hide names, manually enter the list of characters separated by commas.
                </li>
            </ul>
            <h1 className="text-lg font-bold p-10">Disclaimer</h1>
            <p className="text whitespace-pre-line">
                Generated IDs are pulled randomly from the books, and so may not reflect the passages which are most likely to be tested/which are most important to know. 
                Use this as a study tool, but don't let this replace your reading!
            </p>
        </div>
    );
}