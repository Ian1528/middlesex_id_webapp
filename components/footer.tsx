import Link from "next/link";
import { Separator } from "./ui/separator";


export default function Footer() {
  return (
    <footer className="fixed bottom-0 bg-muted py-4 border-t w-screen px-6 items-center justify-center">
        <div className="flow-root w-full items-center text-center gap-1 text-sm text-muted-foreground">
          <Separator orientation="vertical" />
          <p className="float-left">Developed by Ian Lam</p>
          <Separator orientation="vertical" />
          <p className="float-right">
          <Link href="/help" className="hover:underline">
            Help
          </Link>
          </p>
        </div>
    </footer>
  );
}
