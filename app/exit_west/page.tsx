"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { SetStateAction, useState } from "react";

export default function Page() {
  const [id, setId] = useState<string | null>(null);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">

      <div className="grid grid-cols-2 items-center justify-center m-3 gap-3">
        <div>
          <GenerateID_Button setID={setId} />
          {id && (
            <div className="items-center p-10">
              <p className="mb-6 whitespace-normal">{id}</p>
            </div>
          )}
        </div>
        <div>
          <h1 className="grid place-items-center pb-4">
            Check your answers with Ctrl+F and the Exit West textfile below
          </h1>
          <div className="">
            <iframe
              src="/exit_west_textfile.txt"
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

function GenerateID_Button({
  setID,
}: {
  setID: React.Dispatch<SetStateAction<string | null>>;
}) {
  const [words, setWords] = useState<number>(30);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsGenerating(true);
    // fetch the textfile from public directory

    fetch("/api/python/general/get_ID/?n=" + words + "&filename=exit_west_textfile.txt" + "&names=")
      .then((response) => {
        console.log(response);
        return response.json()
      }
      )
      .then((data) => {
        setID(data);
        console.log(data);
      });
    setIsGenerating(false);
  };
  return (
    <form onSubmit={handleFormSubmit}>
      <div className="flex flex-col m-4 gap-4">
        <div>
          <h1 className="grid place-items-center pb-4 font-bold">
            Choose the minimum number of words for the ID
          </h1>
          <Label htmlFor="lines">Minimum Words</Label>
          <Input
            type="number"
            id="lines"
            value={words}
            onChange={(e) => setWords(Number(e.target.value))}
            required
          />
        </div>
        <Button disabled={isGenerating}>
          {!isGenerating ? "Generate ID" : "Generating ID..."}
        </Button>
      </div>
    </form>
  );
}
