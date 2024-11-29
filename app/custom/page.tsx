"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { SetStateAction, useState } from "react";
import UploadPDF from "@/components/PDFUpload";

export default function Page() {
  const [textFile, setTextFile] = useState<string | null>(null);
  const [id, setId] = useState<string | null>(null);

  return (
    <div className="grid grid-cols-2 items-center min-h-screen gap-2 max-w-max mx-auto">
        {
          textFile && (
            <div>
            <GenerateID_Button setID={setId} />
            {id && (
              <div className="items-center p-10">
                <p className="mb-6 whitespace-pre-line">{id}</p>
              </div>
            )}
          </div>
          )
        }
        <div className="items-center justify-center m-auto">
        <UploadPDF textFile={textFile} setTextFile={setTextFile}/>
        </div>

    </div>
  );
}

function GenerateID_Button({setID}: {setID: React.Dispatch<SetStateAction<string | null>>}) {
  const [lines, setLines] = useState<number>(0);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsGenerating(true);
    // fetch the textfile from public directory
    
    fetch("/api/python/custom/get_ID/" + lines)
      .then((response) => response.json())
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
            Choose the minimum number of lines for the ID
          </h1>
          <Label htmlFor="lines">Minimum Lines</Label>
          <Input
            type="number"
            id="lines"
            value={lines}
            onChange={(e) => setLines(Number(e.target.value))}
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
