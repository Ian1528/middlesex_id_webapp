"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { SetStateAction, useState, useEffect } from "react";
import UploadTextfile from "@/components/fileUpload";
export default function Page() {
  const [textFile, setTextFile] = useState<string | null>(null);
  const [id, setId] = useState<string | null>(null);

  return (
    <div className={textFile ? "grid grid-cols-2 items-center min-h-screen gap-2 max-w-max mx-auto" : "grid grid-cols-1 items-center min-h-screen gap-2 max-w-max mx-auto"}>
        {
          textFile && (
            <div>
            <Generate_ID_Button setID={setId} />
            {id && (
              <div className="items-center p-10">
                <p className="mb-6 whitespace-pre-line">{id}</p>
              </div>
            )}
          </div>
          )
        }
        <div className="items-center justify-center m-auto">
        <UploadTextfile textFile={textFile} setTextFile={setTextFile}/>
        </div>

    </div>
  );
}

function Generate_ID_Button({setID}: {setID: React.Dispatch<SetStateAction<string | null>>}) {
  const [lines, setLines] = useState<number>(40);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [names, setNames] = useState<string>("");

  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsGenerating(true);
    const response = await fetch("/api/python/get_custom_ID/?n=" + lines + "&names=" + names)
    const data = await response.json();
    setID(data);

    setIsGenerating(false);
  };
  return (
    <form onSubmit={handleFormSubmit}>
      <div className="flex flex-col m-4 gap-4">
        <div>
          <h1 className="grid place-items-center pb-4 font-bold ">
            Configuration Settings
          </h1>
          <Label htmlFor="lines">Minimum Words</Label>
          <Input
            type="number"
            id="lines"
            value={lines}
            onChange={(e) => setLines(Number(e.target.value))}
            required
          />
          <Label htmlFor="names">Names to blur (enter comma separated values)</Label>
          <Input
            type="text"
            id="names"
            value={names}
            placeholder="ex: John, Jane, Mary"
            onChange={(e) => setNames(e.target.value)}
          />
        </div>
        <Button disabled={isGenerating} type="submit">
          {!isGenerating ? "Generate ID" : "Generating ID..."}
        </Button>
      </div>
    </form>
  );
}
