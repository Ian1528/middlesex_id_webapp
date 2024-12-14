import GenerateID_Button from "./generateID";

export default function GeneralBookPage({
  bookSrc,
  names,
  formatSrc,
}: {
  bookSrc: string;
  names: string;
  formatSrc: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
        <header>
          <p className="text-xs text-left p-5">
            Disclaimer: these IDs are pulled randomly from the books, and so may
            not reflect the passages which are most likely to be tested/which
            are most important to know. Use this as a study tool, but don't let
            this replace your reading!
          </p>
        </header>
      <div className="grid grid-cols-2 items-center justify-center m-3 gap-3">
        <div>
          <GenerateID_Button names_to_hide={names} formatSrc={formatSrc} />
        </div>
        <div>
          <h1 className="grid place-items-center pb-4">
            Check your answers with Ctrl+F. Note! If this doesn't work, trying
            using Chrome instead of Safari.
          </h1>
          <div className="">
            <iframe
              src={bookSrc}
              width="600"
              height="800"
              className="border-2 border-gray-300"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  );
}
