"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { useState } from "react";
export default function Generate_ID_Button({
     names_to_hide, formatSrc
  }: {
      names_to_hide: string;
      formatSrc: string;
  }) {
    const [id, setID] = useState<string | null>(null);
    const [words, setWords] = useState<number>(40);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);
    const [hideNames, sethideNames] = useState<boolean>(true);
    const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setIsGenerating(true);
      // fetch the textfile from public directory
      let names = "";
      if(hideNames){
          names = names_to_hide
      }
      const response = await fetch("/api/python/general_public/get_ID/?n=" + words + "&filename=" + formatSrc + "&names=" + names)
      const data = await response.json();
      setID(data);
  
      setIsGenerating(false);
    };
    return (
      <div>
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
          <Switch id="hide_names" checked={hideNames} onCheckedChange={() => sethideNames(!hideNames)} />
          <Label htmlFor="hide_names">Hide Names</Label>
        </div>
      </form>
        {id && (
            <div className="items-center p-10">
              <p className="mb-6 whitespace-pre-line">{id}</p>
            </div>
          )}
      </div>
    );
  }
  