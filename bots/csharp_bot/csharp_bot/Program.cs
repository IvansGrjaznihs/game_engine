using System.Text;
using System.Text.Json; // Для парсинга JSON
using System.Text.Json.Serialization;

namespace CSharpBot
{
    // Модель входных данных
    public class InputData
    {
        [JsonPropertyName("boardSize")]
        public int BoardSize { get; set; }  // можно использовать, если нужно

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

    // Модель для последнего хода соперника
    public class Move
    {
        [JsonPropertyName("row")]
        public int Row { get; set; }

        [JsonPropertyName("col")]
        public int Col { get; set; }
    }

    // Модель выходных данных (ответ бота)
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
            // Читаем всё из stdin
            string inputJson = Console.In.ReadToEnd();

            // Парсим
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
                // Невалидный JSON
                Console.WriteLine("{\"error\":\"JSON parse error\"}");
                return;
            }

            // Действуем: ищем случайный пустой ход (для примера)
            // Или можно реализовать любую стратегию
            var random = new Random();
            var board = inputData.Board;

            // Собираем список пустых клеток
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
                // Нет свободных клеток — вернём ход -1,-1 (нас дисквалифицируют, но что поделать)
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

            // Серриализуем в JSON
            string outputJson = JsonSerializer.Serialize(response);

            // Вывод в stdout
            Console.OutputEncoding = Encoding.UTF8;
            Console.WriteLine(outputJson);
        }
    }
}
