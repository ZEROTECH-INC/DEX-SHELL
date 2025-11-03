// core/dex_runtime.cs
// .NET 6 console app skeleton
// dotnet new console -o core && replace Program.cs with this content

using System;
using System.Threading;
using System.Threading.Tasks;

namespace DexRuntime {
    class Program {
        static bool running = true;
        static async Task Main(string[] args) {
            Console.WriteLine("DEX Runtime (C#) starting...");
            Console.CancelKeyPress += (sender, e) => {
                running = false;
                e.Cancel = true;
            };

            await RunLoop();
            Console.WriteLine("DEX Runtime exiting.");
        }

        static async Task RunLoop() {
            int tick = 0;
            while (running) {
                Console.WriteLine($"[dex_runtime] tick={tick++}");
                await Task.Delay(1000);
            }
        }
    }
}
