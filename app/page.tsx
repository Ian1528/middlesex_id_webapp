import Image from 'next/image'
import Link from 'next/link'
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
export default function Home() {
  return (
    <div className="flex flex-col items-center min-h-screen p-3">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Middlesex ID Generator!</h1>
      <p className="text-xl mb-8 text-center max-w-2xl">
        Choose one of the options below to get started, or click "help" for instructions
      </p>
      <div className="grid grid-cols-4 gap-3">
        <div className="flex flex-col col-start-1 gap-3">
          <BookCard link="tewwg" title="Their Eyes Were Watching God" grade="9"/>
        </div>
        <div className="flex flex-col col-start-2 gap-3">
          <BookCard link="iliad" title="Iliad" grade="10"/>
          <BookCard link="exit_west" title="Exit West" grade="10"/>
          <BookCard link="pride_and_prejudice" title="Pride and Prejudice" grade="10"/>
        </div>
        <div className="flex flex-col col-start-3 gap-3">
          <BookCard link="hamlet" title="Hamlet" grade="11"/>
        </div>
        <div className="flex flex-col col-start-4 gap-4">
          <BookCard link="custom" title='Custom' grade="NONE"/>
        </div>
      </div>
    </div>
  );
}

function BookCard({ link, title, grade }: { link: string, title: string, grade: string }) {
  return (
    <Link href={`/${link}`}>
      <Card className={`grid bg-white rounded-lg shadow-md col-start-2`} >
        <CardContent className="p-6">
          <div className="flex flex-col gap-3 items-center text-center justify-between mb-4">
            <h2 className="text-xl font-bold text-[#000000]">
              {title}
            </h2>
            <GradeLevel grade={grade} />
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

function GradeLevel({
  grade,
}: {
  grade: string;
}) {
  if (grade === "9") {
    return (
      <div className="bg-[#e6f7f2] text-[#1abc9c] font-medium px-3 py-1 rounded-full text-sm">
        9th Grade
      </div>
    );
  } else if (grade === "10") {
    return (
      <div className="bg-[#fef7f2] text-[#e67e22] font-medium px-3 py-1 rounded-full text-sm">
        10th Grade
      </div>
    );
  } else if (grade === "11"){
      return (
      <div className="bg-[#f2f7fe] text-[#3498db] font-medium px-3 py-1 rounded-full text-sm">
        11th Grade
      </div>
    );
  }
  else if (grade === "NONE"){
    return (
      <div className="bg-[#f2f7fe] text-[#FF0000] font-medium px-3 py-1 rounded-full text-sm">
        Custom
      </div>
    );
  }
  else {
    return (
      <div className="bg-[#f2f7fe] text-[#CF9FFF] font-medium px-3 py-1 rounded-full text-sm">
        12th Grade
      </div>
    );
  }
}
