public class Zombie : IMonster
{
    private int life = 150;

    public int Attack()
    {
        int damage = 15;
        Console.WriteLine($"O zumbi morde ferozmente, causando {damage} de dano!");
        return damage;
    }

    public int Defend()
    {
        int defense = 10;
        Console.WriteLine($"O corpo em decomposição do zumbi absorve parte do dano, reduzindo {defense}.");
        return defense;
    }

    public int SuperAttack()
    {
        int superDamage = 40;
        Console.WriteLine($"O zumbi usa seu Super Ataque: Invocação de Horda, causando {superDamage} de dano!");
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
        Console.WriteLine($"O Zumbi agora tem {life} de vida.");
    }
}
