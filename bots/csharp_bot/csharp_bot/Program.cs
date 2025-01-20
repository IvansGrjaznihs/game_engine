using System.Text;
using System.Text.Json; // JSON parsing
using System.Text.Json.Serialization;

namespace CSharpBot
{
    // Input Data model
    public class InputData
    {
        [JsonPropertyName("boardSize")]
        public int BoardSize { get; set; }

        [JsonPropertyName("board")]
        public string[][] Board { get; set; } = default!;

        [JsonPropertyName("mySymbol")]
        public string MySymbol { get; set; } = "X";

        [JsonPropertyName("opponentSymbol")]
        public string OpponentSymbol { get; set; } = "O";

        [JsonPropertyName("lastMoveOpponent")]
        public Move? LastMoveOpponent { get; set; }

        [JsonPropertyName("moveNumber")]
        public int MoveNumber { get; set; }
    }

    // Opponent's last move model
    public class Move
    {
        [JsonPropertyName("row")]
        public int Row { get; set; }

        [JsonPropertyName("col")]
        public int Col { get; set; }
    }

    // Bot Response model
    public class BotResponse
    {
        [JsonPropertyName("move")]
        public Move Move { get; set; } = default!;

        [JsonPropertyName("debug")]
        public string? DebugInfo { get; set; }
    }

    public static class Program
    {
        public static void Main(string[] args)
        {
            // Read input JSON from stdin
            string inputJson = Console.In.ReadToEnd();

            // Parse input JSON
            InputData? inputData;
            try
            {
                inputData = JsonSerializer.Deserialize<InputData>(inputJson);
                if (inputData == null)
                {
                    // Если десериализация вернула null
                    Console.WriteLine("{\"error\":\"Invalid input data\"}");
                    return;
                }
            }
            catch
            {
                // Not a valid JSON
                Console.WriteLine("{\"error\":\"JSON parse error\"}");
                return;
            }

            // Do: implement your bot logic here
            var random = new Random();
            var board = inputData.Board;

            // Get all empty cells
            List<Move> emptyCells = new();
            for (int r = 0; r < board.Length; r++)
            {
                for (int c = 0; c < board[r].Length; c++)
                {
                    if (string.IsNullOrEmpty(board[r][c]))
                    {
                        emptyCells.Add(new Move { Row = r, Col = c });
                    }
                }
            }

            Move chosenMove;
            if (emptyCells.Count == 0)
            {
                // No empty cells. Return -1, -1
                chosenMove = new Move { Row = -1, Col = -1 };
            }
            else
            {
                chosenMove = emptyCells[random.Next(emptyCells.Count)];
            }

            var response = new BotResponse
            {
                Move = chosenMove,
                DebugInfo = $"Random move for {inputData.MySymbol}"
            };

            // Serialize response to JSON
            string outputJson = JsonSerializer.Serialize(response);

            // Output response JSON to stdout
            Console.OutputEncoding = Encoding.UTF8;
            Console.WriteLine(outputJson);
        }
    }
}
