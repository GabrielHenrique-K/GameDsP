public class Dragon : IMonster
{
    private int life = 200;

    public int Attack()
    {
        int damage = 30;
        Console.WriteLine($"O dragão cospe fogo, causando {damage} de dano!");
        return damage;
    }

    public int Defend()
    {
        int defense = 20;
        Console.WriteLine($"O dragão usa suas escamas resistentes para se defender, reduzindo {defense} de dano.");
        return defense;
    }

    public int SuperAttack()
    {
        int superDamage = 50;
        Console.WriteLine($"O dragão usa seu Super Ataque: Chuva de Chamas, causando {superDamage} de dano!");
        return superDamage;
    }

    public int Life()
    {
        return life;
    }

    public void TakeDamage(int damage)
    {
        life -= damage;
        if (life < 0) life = 0;
        Console.WriteLine($"O Dragão agora tem {life} de vida.");
    }
}
