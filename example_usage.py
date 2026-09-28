from client import AgentPromptInjectionJailbreakSentinel
import json

def main():
    sentinel = AgentPromptInjectionJailbreakSentinel()
    res = sentinel.run_benchmark_jailbreak_sentinel()
    print("Prompt Injection Sentinel Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
