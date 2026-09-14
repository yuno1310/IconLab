# Three-minute evidence replay script

Synthetic voice narration; recorded results, not a live screen recording.

## Scene 1

Harbor Devices is a fictional distributor whose analysts search separate policy files before answering support questions. A fluent answer can still contain an old deadline or miss a conflict. This demo shows why the project scores retrieval and generation separately. Every result shown is a replay of a recorded local model run, using synthetic data.

## Scene 2

Here is a simple owner lookup. The baseline returns Mira and passes. The improved model also names Mira, but invents an invalid source identifier. Its validator rejects that answer. This is a real regression, not a polished success-only demo. Retrieving the right document IDs does not prove a model will produce valid citations.

## Scene 3

Now consider conflicting return policies. The baseline quotes two windows but omits the required conflict resolution. The improved answer explains that neither bulletin establishes precedence and that a support lead must resolve the conflict. Both systems recovered the required source IDs. That is why the separate generation column provides a useful diagnostic signal.

## Scene 4

The annual revenue question has no answer in the corpus. The baseline invents one hundred million dollars and attaches policy citations that do not support it. The improved query coverage guard declines before calling the model. Across ten must-refuse cases it passes all ten. This guard is lexical, so paraphrases and adversarial queries still need testing.

## Scene 5

The complete model comparison covers fifty questions. Baseline retrieval passes thirty and generation passes fifteen. Improved retrieval passes all fifty, while generation passes thirty eight. Ten improved responses encounter execution or citation validation errors and count as failures. The dataset and corpus were jointly authored, so these results are development evidence rather than independent validation.

## Scene 6

The security evidence shows analyst A reading analyst B’s case before the fix. The served version checks ownership and returns case unavailable. A thousand-call exercise originally accepted every call. With the quota, twenty calls pass and nine hundred eighty fail in one simulated minute. Restarting the process resets that quota. Remote authentication is not implemented.

## Scene 7

The package includes the source, golden set, setup guide, transcripts, and exported Langfuse observations. Generation latency in the final improved run is about seven hundred forty four milliseconds at the median, and nineteen hundred seventy seven at the ninety fifth percentile. Human sign-off, a second-person clean setup, GitHub publication, and team submission are still pending.
