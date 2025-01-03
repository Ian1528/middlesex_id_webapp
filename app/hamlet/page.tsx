"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { SetStateAction, useState } from "react";
import { Switch } from "@/components/ui/switch";
export default function Page() {
  const [id, setId] = useState<string | null>(null);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <header>
        <p className="text-xs text-left p-5">
          Disclaimer: these IDs are pulled randomly from the books, and so may not reflect the passages which are most likely to be tested/which are most important to know. 
          Use this as a study tool, but don't let this replace your reading!
        </p>
      </header>
      <div className="grid grid-cols-2 items-center justify-center m-3 gap-3">
        <div>
          <GenerateID_Button setID={setId} />
          {id && (
            <div className="items-center p-10">
              <p className="mb-6 whitespace-pre-line">{id}</p>
            </div>
          )}
        </div>
        <div>
          <h1 className="grid place-items-center pb-4">
            Check your answers with Ctrl+F and the Hamlet PDF below. If this doesn't work, trying using Chrome instead of Safari.
          </h1>
          <div className="">
            <iframe
              src="/hamlet_pdf.pdf"
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

function GenerateID_Button({setID}: {setID: React.Dispatch<SetStateAction<string | null>>}) {
  const [words, setWords] = useState<number>(30);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [hideNames, sethideNames] = useState<boolean>(true);

  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsGenerating(true);
    // fetch the textfile from public directory
    
    const response = await fetch("/api/python/hamlet/get_ID/?n=" + words + "&hide_names=" + hideNames);
    const data = await response.json();
    setID(data);
    
    setIsGenerating(false);
  };
  return (
    <form onSubmit={handleFormSubmit}>
      <div className="flex flex-col m-4 gap-4">
        <div>
          <h1 className="grid place-items-center pb-4 font-bold">
            Choose the minimum number of words for the ID
          </h1>
          <Label htmlFor="words">Minimum Words</Label>
          <Input
            type="number"
            id="words"
            value={words}
            onChange={(e) => setWords(Number(e.target.value))}
            required
          />
        </div>
        <Button disabled={isGenerating}>
          {!isGenerating ? "Generate ID" : "Generating ID..."}
        </Button>
        <Switch id="hide_names" checked={hideNames} onCheckedChange={() => sethideNames(!hideNames)} />
        <Label htmlFor="hide_names">Hide Names</Label>
      </div>
    </form>
  );
}
