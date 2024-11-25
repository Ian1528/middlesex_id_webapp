import Image from 'next/image'
import Link from 'next/link'
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Hamlet ID Generator!</h1>
      <p className="text-xl mb-8 text-center max-w-2xl">
        Click the button below to get started
      </p>
      <Link href="/hamlet" passHref>
        <Button className="px-6 py-2">Get Started</Button>
      </Link>
    </div>
  );
}
