"use client";
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from './ui/input';

const UploadTextfile = ({ textFile, setTextFile } : { textFile: string | null, setTextFile: React.Dispatch<React.SetStateAction<string | null>>
}) => {
  const [file, setFile] = useState<File>();
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) {
      return;
    }
    else{
        setFile(e.target.files[0]);
    }
  }
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      return;
    }
    try{
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch('/api/python/upload_text', {
            method: 'POST',
            body: formData,
        });
        console.log("response", response);
        if (!response.ok) {
            throw new Error('File upload failed');
        }
        
        const data = await response.json();
        console.log("data", data);
        setTextFile(data.content);

      // Handle successful upload (e.g., display a success message)
    } catch (error) {
        console.error(error);
      // Handle upload error (e.g., display an error message)
    }
  };

  const closeSession = async () => {
    await fetch("/api/python/close_session", { method: "POST" });
  }
  useEffect(() => {
    window.addEventListener("beforeunload", closeSession);
    return () => {
      window.removeEventListener("beforeunload", closeSession);
      closeSession();
    };
  }, []);

  return (
    <div>
      <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-3 p-2">
              <h1 className="grid place-items-center pb-4 font-bold">
                  Upload Text File
              </h1>
              <Input
                  type="file"
                  id="file"
                  name="file"
                  accept="text/plain"
                  onChange={handleFileChange}
              />
              <Button type="submit" variant="outline">Submit</Button>
          </div>
      </form>
      {textFile && (
        <div className="flex flex-col max-w-max">
          <h3>Preview</h3>
          <textarea readOnly value={textFile} rows={10} cols={75}></textarea>
        </div>
      )}
    </div>
  );
};

export default UploadTextfile;