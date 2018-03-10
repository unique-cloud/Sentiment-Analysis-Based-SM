class CreateCombinations < ActiveRecord::Migration[5.1]
  def change
    create_table :combinations do |t|
      t.integer :micropost_id
      t.integer :tag_id

      t.timestamps
    end
  end
end
