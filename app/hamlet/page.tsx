"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { SetStateAction, useState } from "react";

export default function Page() {
  const [id, setId] = useState<string | null>(null);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <GenerateID_Button setID={setId}/>
      {id && 
      <div className="items-center p-10">
        <p className="mb-6 whitespace-pre-line">{id}</p>
      </div>
      }
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
    
    fetch("/api/python/get_ID/" + lines)
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
